from pathlib import Path
import shutil


def main():
    root = Path(__file__).resolve().parents[1]
    final_cfg = root / "FINAL" / "configs"
    final_cfg.mkdir(parents=True, exist_ok=True)

    # Final declared config set
    shutil.copy2(root / "configs" / "injection_v2_R001.yaml", final_cfg / "final_injection_config.yaml")
    shutil.copy2(root / "configs" / "eval_config.yaml", final_cfg / "final_eval_config.yaml")
    shutil.copy2(root / "configs" / "week09_proposed.yaml", final_cfg / "final_proposed_config.yaml")

    print("Week12 final config set frozen in FINAL/configs/")


if __name__ == "__main__":
    main()