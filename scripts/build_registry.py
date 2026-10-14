#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyyaml>=6.0.1",
# ]
# ///
"""
Scans `skills/*/SKILL.md` and updates the root `README.md` with an up-to-date
Skill Catalog Table and one-click install commands.
"""
import re
from pathlib import Path
import yaml

REPO_URL = "https://github.com/logeshv586-code/AIproductfactory"
START_MARKER = "<!-- SKILL_REGISTRY_START -->"
END_MARKER = "<!-- SKILL_REGISTRY_END -->"


def parse_skill(skill_dir: Path) -> dict | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    try:
        fm = yaml.safe_load(match.group(1)) if match else {}
    except yaml.YAMLError:
        # Existing third-party skills may have nonconforming quoted frontmatter.
        # Keep their registry entries without modifying source skill text.
        from validate_skills import parse_simple_frontmatter
        fm = parse_simple_frontmatter(text)
    if not isinstance(fm, dict):
        fm = {}
    name = str(fm.get("name") or skill_dir.name)
    desc = str(fm.get("description") or "Modular AI Agent Skill").strip().replace("\n", " ").replace("|", "\\|")
    if desc in ("|", ">", "|-", ">-"):
        from validate_skills import parse_simple_frontmatter
        desc = parse_simple_frontmatter(text).get("description", "Modular AI Agent Skill").replace("|", "\\|")
    has_scripts = "✅" if (skill_dir / "scripts").exists() else "—"
    has_refs = "✅" if (skill_dir / "references").exists() else "—"
    install_cmd = f"`npx skills add {REPO_URL} --skill {name}`"
    return {
        "name": name,
        "folder": skill_dir.name,
        "description": desc[:140] + ("..." if len(desc) > 140 else ""),
        "scripts": has_scripts,
        "refs": has_refs,
        "install": install_cmd,
    }


def generate_table(skills: list[dict]) -> str:
    lines = [
        START_MARKER,
        "| Skill | Description | Scripts | References | One-Click Install |",
        "| :--- | :--- | :---: | :---: | :--- |",
    ]
    for s in skills:
        link = f"[**{s['name']}**](skills/{s['folder']})"
        lines.append(
            f"| {link} | {s['description']} | {s['scripts']} | {s['refs']} | {s['install']} |"
        )
    lines.append(END_MARKER)
    return "\n".join(lines)


def main():
    skills_root = Path("skills")
    skills = []
    if skills_root.exists():
        for d in sorted(skills_root.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                parsed = parse_skill(d)
                if parsed:
                    skills.append(parsed)

    table_md = generate_table(skills)
    readme_path = Path("README.md")

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if START_MARKER in content and END_MARKER in content:
            pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
            updated = pattern.sub(table_md, content)
        else:
            updated = content.rstrip() + "\n\n## Automated Skill Registry\n\n" + table_md + "\n"
    else:
        updated = f"# AI Product Factory\n\nCentralized hub of modular, schema-validated AI Agent Skills.\n\n## Automated Skill Registry\n\n{table_md}\n"

    readme_path.write_text(updated, encoding="utf-8")
    print(f"✅ Updated README.md with {len(skills)} indexed skills.")


if __name__ == "__main__":
    main()