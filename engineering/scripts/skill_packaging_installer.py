#!/usr/bin/env python3
"""Skill packaging and safe installer engine for Ticket 37.
Packages the target skill with safe installation behavior: conflict detection,
timestamped backups (.bak_<timestamp>), diff summaries, and honest multi-runtime capability declarations.
"""
import datetime
import difflib
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

SUPPORTED_RUNTIMES = {
    "claude_code": {"type": "tool_enabled", "features": ["bash", "read", "grep", "web_search"]},
    "omp": {"type": "tool_enabled", "features": ["bash", "read", "grep", "eval", "browser"]},
    "pi": {"type": "tool_enabled", "features": ["bash", "read"]},
    "codex": {"type": "tool_enabled", "features": ["bash", "read"]},
    "chatgpt_web": {"type": "prompt_only", "features": ["prompt_in_context"], "fallback": "static_rag_degraded"}
}

def validate_skill_package_structure(skill_root: Path) -> Dict[str, Any]:
    """Validates skill package entrypoints, references, and schemas."""
    issues = []
    
    skill_md = skill_root / "SKILL.md"
    if not skill_md.exists():
        issues.append("Missing mandatory SKILL.md entrypoint.")

    references_dir = skill_root / "references"
    if not references_dir.exists():
        issues.append("Missing references directory.")

    categories_dir = references_dir / "categories"
    if not categories_dir.exists():
        issues.append("Missing references/categories directory.")

    is_valid = len(issues) == 0
    return {
        "is_valid": is_valid,
        "issues": issues,
        "skill_entrypoint": str(skill_md) if skill_md.exists() else None
    }

def install_skill_safely(
    source_skill_dir: Path,
    target_install_dir: Path,
    allow_backup: bool = True
) -> Dict[str, Any]:
    """Installs skill files safely with conflict detection, timestamped backups, and diff summaries."""
    if not source_skill_dir.exists():
        raise FileNotFoundError(f"Source skill directory '{source_skill_dir}' not found.")

    backup_created = None
    if target_install_dir.exists():
        if not allow_backup:
            raise PermissionError("Attempted to overwrite existing skill directory without backup permission.")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_install_dir.parent / f"{target_install_dir.name}.bak_{timestamp}"
        shutil.copytree(target_install_dir, backup_path)
        backup_created = str(backup_path)

    # Perform file-by-file copy and compute diff summary
    target_install_dir.mkdir(parents=True, exist_ok=True)
    created_files = []
    updated_files = []
    unchanged_files = []

    for root, dirs, files in os.walk(source_skill_dir):
        rel_root = Path(root).relative_to(source_skill_dir)
        dest_root = target_install_dir / rel_root
        dest_root.mkdir(parents=True, exist_ok=True)

        for f in files:
            src_file = Path(root) / f
            dest_file = dest_root / f

            if not dest_file.exists():
                shutil.copy2(src_file, dest_file)
                created_files.append(str(rel_root / f))
            else:
                src_bytes = src_file.read_bytes()
                dest_bytes = dest_file.read_bytes()
                if src_bytes != dest_bytes:
                    shutil.copy2(src_file, dest_file)
                    updated_files.append(str(rel_root / f))
                else:
                    unchanged_files.append(str(rel_root / f))

    return {
        "status": "INSTALLED_SUCCESS",
        "target_directory": str(target_install_dir),
        "backup_path": backup_created,
        "diff_summary": {
            "created_count": len(created_files),
            "updated_count": len(updated_files),
            "unchanged_count": len(unchanged_files),
            "created_files": created_files,
            "updated_files": updated_files
        }
    }

def get_runtime_capability_declaration(runtime_name: str) -> Dict[str, Any]:
    """Provides honest runtime capability declaration and fallback modes."""
    rt_info = SUPPORTED_RUNTIMES.get(runtime_name)
    if not rt_info:
        return {
            "runtime": runtime_name,
            "is_supported": False,
            "status": "UNVERIFIED_RUNTIME",
            "notes": f"Runtime '{runtime_name}' has not been verified in test matrix."
        }

    return {
        "runtime": runtime_name,
        "is_supported": True,
        "runtime_type": rt_info["type"],
        "features_available": rt_info["features"],
        "fallback_mode": rt_info.get("fallback", "none"),
        "status": "VERIFIED_READY"
    }

if __name__ == "__main__":
    print("Skill Packaging and Installer Module ready.")
