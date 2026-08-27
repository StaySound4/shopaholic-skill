#!/usr/bin/env python3
"""Executable evaluation seam runner.
Executes or records a shopping recommendation run for an evaluation case,
capturing verbatim output, metadata, tool traces, and structured decision records
strictly conforming to run-record.schema.json.
"""
import argparse, datetime, hashlib, json, os, re, sys, uuid
from pathlib import Path

def extract_decision_record_xml(raw_text: str) -> str | None:
    match = re.search(r'<decision_record>(.*?)</decision_record>', raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def validate_against_schema(data: dict, schema_path: Path | None = None) -> list[str]:
    """Validates run-record against schema definition."""
    errors = []
    if schema_path is None:
        schema_path = Path(__file__).resolve().parents[1] / "schemas/run-record.schema.json"
        
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            required = schema.get("required", [])
            for req in required:
                if req not in data or data[req] is None:
                    errors.append(f"Missing required field: {req}")
            
            valid_statuses = schema.get("properties", {}).get("status", {}).get("enum", [])
            status = data.get("status")
            if valid_statuses and status not in valid_statuses:
                errors.append(f"Invalid status '{status}', must be one of {valid_statuses}")
        except Exception as e:
            errors.append(f"Failed to read/parse schema: {e}")
    else:
        # Fallback if schema file cannot be loaded
        required = ["run_id", "case_id", "condition", "replicate", "started_at", "status", "raw_output_path"]
        for req in required:
            if req not in data or data[req] is None:
                errors.append(f"Missing required field: {req}")
        
    if "replicate" in data and (not isinstance(data["replicate"], int) or data["replicate"] < 1):
        errors.append("Field 'replicate' must be an integer >= 1")
        
    return errors
def create_run_record(
    case_id: str,
    condition: str,
    replicate: int,
    raw_output: str,
    output_dir: Path,
    status: str = "complete",
    model: str | None = None,
    runtime: str | None = None,
    skill_hash: str | None = None,
    tools: list[str] | None = None,
    tool_trace: list[dict] | None = None,
    tokens: int | None = None,
    search_count: int | None = None,
    notes: str | None = None
) -> dict:
    run_id = f"run_{case_id}_{condition}_r{replicate}_{uuid.uuid4().hex[:8]}"
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    raw_output_file = run_dir / "raw_output.txt"
    raw_output_file.write_text(raw_output, encoding="utf-8")
    
    xml_content = extract_decision_record_xml(raw_output)
    decision_record_file = None
    if xml_content:
        decision_record_file = run_dir / "decision_record.json"
        try:
            parsed_json = json.loads(xml_content)
            decision_record_file.write_text(json.dumps(parsed_json, indent=2, ensure_ascii=False), encoding="utf-8")
        except json.JSONDecodeError:
            decision_record_file.write_text(xml_content, encoding="utf-8")
            
    tool_trace_file = None
    if tool_trace is not None:
        tool_trace_file = run_dir / "tool_trace.json"
        tool_trace_file.write_text(json.dumps(tool_trace, indent=2, ensure_ascii=False), encoding="utf-8")
        
    ended_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # normalize status to schema enum if needed
    normalized_status = "complete" if status == "COMPLETED" else status
    
    record = {
        "run_id": run_id,
        "case_id": case_id,
        "condition": condition,
        "replicate": replicate,
        "model": model,
        "runtime": runtime,
        "skill_hash": skill_hash,
        "tools": tools or [],
        "started_at": started_at,
        "ended_at": ended_at,
        "status": normalized_status,
        "raw_output_path": str(raw_output_file.resolve()),
        "tool_trace_path": str(tool_trace_file.resolve()) if tool_trace_file else None,
        "decision_record_path": str(decision_record_file.resolve()) if decision_record_file else None,
        "tokens": tokens,
        "search_count": search_count,
        "notes": notes
    }
    # Validate against schema contract
    schema_path = Path(__file__).resolve().parents[1] / "schemas/run-record.schema.json"
    errs = validate_against_schema(record, schema_path)
    if errs:
        raise ValueError(f"Run record validation failed: {errs}")
        
    run_record_file = run_dir / "run_record.json"
    run_record_file.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return record

def main():
    p = argparse.ArgumentParser(description="Evaluation Seam: Record and preserve LLM run artifacts")
    p.add_argument("--case-id", required=True, help="Evaluation Case ID (e.g. D-001)")
    p.add_argument("--condition", default="B1_uploaded_current", help="Experimental condition identifier")
    p.add_argument("--replicate", type=int, default=1, help="Replicate number (>=1)")
    p.add_argument("--input-file", help="File containing raw output to ingest")
    p.add_argument("--out-dir", default="engineering/evals/runs", help="Output directory for run artifacts")
    p.add_argument("--status", default="complete", choices=["complete", "COMPLETED", "FAIL_PRODUCT", "FAIL_EVALUATOR", "BLOCKED_CAPABILITY", "BLOCKED_SOURCE", "INVALID_PROTOCOL"])
    args = p.parse_args()
    
    if args.input_file:
        raw_text = Path(args.input_file).read_text(encoding="utf-8")
    else:
        raw_text = sys.stdin.read()
        
    rec = create_run_record(
        case_id=args.case_id,
        condition=args.condition,
        replicate=args.replicate,
        raw_output=raw_text,
        output_dir=Path(args.out_dir),
        status=args.status
    )
    print(json.dumps(rec, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
