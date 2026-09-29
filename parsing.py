import json
from typing import Any


class Config:
    def __init__(self) -> None:
        self.DEFAULT_CONFIG: dict[str, Any] = {
            "highscore_filename": "highscores.json",
            "lives": 3,
            "pacgum": 42,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 90,
            "levels": [
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15},
                {"width": 15, "height": 15}
            ]
        }

    def load_config(self, filename: str) -> dict[str, Any]:
        with open(filename, "r") as file:
            lines = []
            for line in file:
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                lines.append(line)
            content = "".join(lines)
        return json.loads(content)

    def check_height_width(
        self,
        width: int,
        height: int
    ) -> tuple[str, bool]:
        if width < 2:
            return "width", False
        if height < 2:
            return "height", False
        if width == 2 and height == 2:
            return "width and height", False
        return "", True

    def check_config(self) -> dict[str, Any]:
        values_dict: dict[str, Any] = {}
        correct_values_dict: dict[str, Any] = {}
        try:
            values_dict = self.load_config("config.json")
        except Exception:
            print("Error in loading file")
            return self.DEFAULT_CONFIG.copy()
        default_keys = list(self.DEFAULT_CONFIG.keys())
        for key in values_dict:
            normalized_key = key.strip().lower()
            if normalized_key in default_keys:
                if normalized_key == "highscore_filename":
                    if isinstance(values_dict[key], str):
                        filename = values_dict[key].strip().lower()
                        if filename.endswith(".json"):
                            correct_values_dict[normalized_key] = filename
                        else:
                            correct_values_dict[normalized_key] = (
                                self.DEFAULT_CONFIG[normalized_key]
                            )
                            print(
                                f"value for {key} is invalid, "
                                "using the default value"
                            )
                    else:
                        correct_values_dict[normalized_key] = (
                            self.DEFAULT_CONFIG[normalized_key]
                        )
                        print(
                            f"value for {key} is invalid, "
                            "using the default value"
                        )
                elif normalized_key in ["lives", "level_max_time"]:
                    try:
                        if (
                            isinstance(values_dict[key], int)
                            and not isinstance(values_dict[key], bool)
                            and values_dict[key] > 0
                        ):
                            correct_values_dict[normalized_key] = values_dict[key]
                        else:
                            correct_values_dict[normalized_key] = (
                                self.DEFAULT_CONFIG[normalized_key]
                            )
                            print(
                                f"value for {key} is invalid, "
                                "using the default value"
                            )
                    except Exception:
                        correct_values_dict[normalized_key] = (
                            self.DEFAULT_CONFIG[normalized_key]
                        )
                        print(
                            f"value for {key} is invalid, "
                            "using the default value"
                        )
                elif normalized_key in [
                    "pacgum",
                    "points_per_pacgum",
                    "points_per_super_pacgum",
                    "points_per_ghost",
                    "seed"
                ]:
                    try:
                        if (
                            isinstance(values_dict[key], int)
                            and not isinstance(values_dict[key], bool)
                            and values_dict[key] >= 0
                        ):
                            correct_values_dict[normalized_key] = values_dict[key]
                        else:
                            correct_values_dict[normalized_key] = (
                                self.DEFAULT_CONFIG[normalized_key]
                            )
                            print(
                                f"value for {key} is invalid, "
                                "using the default value"
                            )
                    except Exception:
                        correct_values_dict[normalized_key] = (
                            self.DEFAULT_CONFIG[normalized_key]
                        )
                        print(
                            f"value for {key} is invalid, "
                            "using the default value"
                        )
                elif normalized_key == "levels":
                    try:
                        level_counter = 0
                        levels_list: list[dict[str, int]] = []
                        if not isinstance(values_dict[key], list):
                            print(
                                "levels is invalid, "
                                "using the default levels"
                            )
                            correct_values_dict[normalized_key] = (
                                self.DEFAULT_CONFIG[normalized_key]
                            )
                            continue
                        for level in values_dict[key]:
                            level_counter += 1
                            if not isinstance(level, dict):
                                print(
                                    f"invalid level {level_counter}, "
                                    "using default values"
                                )
                                levels_list.append(
                                    {"width": 15, "height": 15}
                                )
                                continue
                            level_value_list = [15, 15]
                            for k in level:
                                normalized_level_key = k.strip().lower()
                                if normalized_level_key == "width":
                                    try:
                                        if (
                                            isinstance(level[k], int)
                                            and not isinstance(
                                                level[k], bool
                                            )
                                        ):
                                            level_value_list[0] = level[k]
                                        else:
                                            raise ValueError()
                                    except Exception:
                                        level_value_list[0] = 15
                                        print(
                                            f"using default value of the "
                                            f"width in level {level_counter}"
                                        )
                                elif normalized_level_key == "height":
                                    try:
                                        if (
                                            isinstance(level[k], int)
                                            and not isinstance(
                                                level[k], bool
                                            )
                                        ):
                                            level_value_list[1] = level[k]
                                        else:
                                            raise ValueError()
                                    except Exception:
                                        level_value_list[1] = 15
                                        print(
                                            f"using default value of the "
                                            f"height in level {level_counter}"
                                        )
                                else:
                                    print(
                                        f"unknown key {k} in level "
                                        f"{level_counter}, ignoring"
                                    )
                            message, valid = self.check_height_width(
                                level_value_list[0],
                                level_value_list[1]
                            )
                            if valid:
                                levels_list.append(
                                    {
                                        "width": level_value_list[0],
                                        "height": level_value_list[1]
                                    }
                                )
                            elif message == "width":
                                levels_list.append(
                                    {
                                        "width": 15,
                                        "height": level_value_list[1]
                                    }
                                )
                                print(
                                    f"using default value of the "
                                    f"{message} in level {level_counter}"
                                )
                            elif message == "height":
                                levels_list.append(
                                    {
                                        "width": level_value_list[0],
                                        "height": 15
                                    }
                                )
                                print(
                                    f"using default value of the "
                                    f"{message} in level {level_counter}"
                                )
                            else:
                                levels_list.append(
                                    {"width": 15, "height": 15}
                                )
                                print(
                                    f"using default values of width "
                                    f"and height in level "
                                    f"{level_counter}"
                                )
                        while len(levels_list) < 10:
                            levels_list.append(
                                {"width": 15, "height": 15}
                            )
                        correct_values_dict[normalized_key] = levels_list
                    except Exception as error:
                        print(error)
                        correct_values_dict[normalized_key] = (
                            self.DEFAULT_CONFIG[normalized_key]
                        )
            else:
                print(f"unknown key {key}, ignoring")
        for key in default_keys:
            if key not in correct_values_dict:
                correct_values_dict[key] = self.DEFAULT_CONFIG[key]
                print(
                    f"missing key {key}, "
                    "using the default value"
                )
        return correct_values_dict


config = Config()
values = config.check_config()

for i in values.keys():
    print(f"{i}: {values[i]}")

