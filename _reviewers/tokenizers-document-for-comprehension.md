---
title: Document for comprehension
description: 'Add comprehensive documentation that helps others understand both the
  interface and implementation of your code. This includes:


  1. **Detailed parameter documentation** in docstrings with type information and
  purpose descriptions, especially for new or non-obvious parameters'
repository: huggingface/tokenizers
label: Documentation
language: Python
comments_count: 2
repository_stars: 9868
---

Add comprehensive documentation that helps others understand both the interface and implementation of your code. This includes:

1. **Detailed parameter documentation** in docstrings with type information and purpose descriptions, especially for new or non-obvious parameters
2. **Explanatory comments** for complex logic, algorithms, or when integrating external libraries
3. **Clear examples** when appropriate to demonstrate usage

Example of good parameter documentation:
```python
def train(
    files: List[str],
    vocab_size: int = 8000,
    show_progress: bool = True,
    unk_token: Optional[str] = None,
):
    """
    Train the model using the given files

    Args:
        files (:obj:`List[str]`):
            A list of path to the files that we should use for training
        vocab_size (:obj:`int`):
            The size of the final vocabulary, including all tokens and alphabet.
        show_progress (:obj:`bool`):
            Whether to show progress bars while training.
        unk_token (:obj:`str`, `optional`):
            The unknown token to be used by the model.
    """
```

Example of good implementation comments:
```python
class JiebaPreTokenizer:
    def jieba_split(self, pretoken_index, pretoken):
        new_tokens = []
        # Convert to string to ensure compatibility with jieba tokenizer
        pretoken_string = str(pretoken)
        # Extract tokens using jieba's tokenize function which returns (word, start, end)
        for token, start, stop in jieba.tokenize(pretoken_string):
            new_tokens.append(pretoken[start:stop])
        return new_tokens

    def pre_tokenize(self, pretok):
        # Split the PreTokenizedString using our custom jieba_split function
        # which handles tokenization based on Chinese word boundaries
        pretok.split(self.jieba_split)
```