from pathlib import Path

from typing import Any
import json


class CleanCommentsException(Exception):
    pass


def is_bot(author_name: str) -> bool:
    return "[bot]" in author_name or author_name == "Copilot"


def clean_reviewers_discussions_from_bots(
    reviewer_discussions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    valid_discussions: list[dict[str, Any]] = []
    for discussion in reviewer_discussions:
        discussion_comments = discussion.get("discussion_comments", [])
        valid_comments: list[dict[str, Any]] = []
        for c in discussion_comments:
            if "comment_author" not in c or not c["comment_author"]:
                # this is not a valid comment
                continue
            if is_bot(c["comment_author"]):
                continue
            valid_comments.append(c)
        if not valid_comments:
            # all discussion comments are bots, we should not keep it
            continue
        # override original discussions with filtered discussions
        discussion["discussion_comments"] = valid_comments
        valid_discussions.append(discussion)
    return valid_discussions


def process_reviewer_json(file_path: str) -> bool:
    """Returns True if the reviewer is kept (there are still discussions) and False otherwise"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        cleaned_discussions = clean_reviewers_discussions_from_bots(data)
    except Exception as e:
        print(f"Error cleaning discussions of {file_path}: {e}")
        raise CleanCommentsException(f"Failed to clean discussions in {file_path}")

    if cleaned_discussions:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_discussions, f, indent=2, ensure_ascii=False)
        print(
            f"Processed {file_path}: {len(data)} -> {len(cleaned_discussions)} discussions"
        )
        return True
    else:
        print(f"{file_path}: All discussions were filtered out (only bot comments)")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        return False


def process_all_json_files(
    directory: str = "_reviewers", debug: bool = False
) -> list[str]:
    reviewers_dir = Path(directory)

    json_files = list(reviewers_dir.glob("*.json"))

    to_keep = 0
    to_discard = 0
    reviewers_failed_cleaning: list[str] = []
    reviewers_to_delete: list[Path] = []
    for json_file in sorted(json_files):
        try:
            keep_reviewer = process_reviewer_json(str(json_file))
        except CleanCommentsException:
            reviewers_failed_cleaning.append(json_file)
            continue

        if keep_reviewer:
            to_keep += 1
        else:
            reviewers_to_delete.append(json_file)
            to_discard += 1

    reviewers_to_delete_str = [str(path.stem) for path in reviewers_to_delete]
    reviewers_failed_cleaning_str = [
        str(path.stem) for path in reviewers_failed_cleaning
    ]

    if debug:
        with open("reviewers_to_delete.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "reviewers_to_delete": reviewers_to_delete_str,
                    "reviewers_failed_cleaning": reviewers_failed_cleaning_str,
                },
                f,
                indent=2,
            )

    print("Summary:")
    print(f"Total files: {len(json_files)}")
    print(f"Reviewers to keep: {to_keep}")
    print(f"Reviewers to discard: {to_discard}")
    print(f"Failed cleaning: {len(reviewers_failed_cleaning)} reviewers")

    return reviewers_to_delete_str


def delete_reviewers(names: list[str]) -> None:
    reviewers_dir = Path("_reviewers")
    for name in names:
        (reviewers_dir / f"{name}.json").unlink(missing_ok=True)
        (reviewers_dir / f"{name}.md").unlink(missing_ok=True)


def main() -> None:
    reviewers_to_delete = process_all_json_files(debug=True)
    delete_reviewers(reviewers_to_delete)
    print("Done")


if __name__ == "__main__":
    main()
