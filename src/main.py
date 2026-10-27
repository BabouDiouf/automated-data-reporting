from pathlib import Path
import subprocess
import sys


# ==================================================
# CONFIGURATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"

SCRIPTS = [
    "generate_data.py",
    "explore_data.py",
    "clean_data.py",
    "analyze_data.py",
    "generate_charts.py",
    "generate_report.py",
]


# ==================================================
# EXÉCUTION DU PIPELINE
# ==================================================

def main():
    print("=" * 60)
    print("SUNU MARKET — AUTOMATISATION DU REPORTING COMMERCIAL")
    print("=" * 60)

    for script in SCRIPTS:
        script_path = SRC_DIR / script

        if not script_path.exists():
            print(f"\nERREUR : script introuvable : {script_path}")
            sys.exit(1)

        print(f"\nÉtape en cours : {script}")
        print("-" * 60)

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_DIR
        )

        if result.returncode != 0:
            print(f"\nERREUR : échec de l'exécution de {script}")
            sys.exit(result.returncode)

        print(f"\nÉtape terminée : {script}")

    print("\n" + "=" * 60)
    print("PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 60)
    print("Rapport Excel :", PROJECT_DIR / "reports" / "rapport_commercial.xlsx")


if __name__ == "__main__":
    main()