# How to Contribute

First off, thank you for considering contributing to uTu-agent! It's people like you that make our community and software better. We welcome any and all contributions.

We use GitHub [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to accept contributions.

## Guidelines

To ensure a smooth and effective contribution process, please adhere to the following guidelines:

1.  **Link to an Existing Issue**: All pull requests should be linked to an existing issue. If you're proposing a new feature or a bug fix, please create an issue first to discuss it with the maintainers.
2.  **Keep It Small and Focused**: Avoid bundling multiple features or fixes in a single pull request. Smaller, focused PRs are easier to review and merge.
3.  **Use Draft PRs for Work in Progress**: If your work is not yet ready for review, open it as a [draft pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests#draft-pull-requests). This signals that you're still working on it and prevents premature reviews.
4.  **Ensure All Checks Pass**: Before submitting your PR for review, make sure that all automated checks (like linting and testing) are passing.
5.  **Update Documentation**: If you're adding a new feature or changing an existing one, please update the relevant documentation to reflect your changes.
6.  **Write Clear Commit Messages and a Good PR Description**: A clear description of your changes is crucial. Explain the "what" and the "why" of your contribution, not just the "how".

## Development Workflow

### Environment Setup

For a complete guide on setting up your development environment, please refer to our [Quick Start](https://tencentcloudadp.github.io/youtu-agent/quickstart/) documentation. Here are the essential steps:

```sh
# Install all dependencies
make sync

# Install pre-commit hooks to automatically check your code before committing
pre-commit install

# You can test the hooks at any time by running:
pre-commit run
```

### Formatting & Linting

We use `pre-commit` to automatically format code and run linters on every commit. This helps maintain a consistent code style across the project.

While the hooks run automatically, we also recommend running the formatting and linting checks manually before you commit your changes. This can help you catch and fix issues earlier.

```sh
# Format code and run linters
make format
```

### Testing

Ensure your changes are covered by tests. If you've modified a specific component, like the search toolkit, you can run its specific tests:

```sh
pytest tests/tools/test_search_toolkit.py
```

To run the entire test suite:

```sh
pytest
```

### Submitting Your Pull Request

Once your changes are ready, tested, and linted, commit your code and open a pull request on GitHub. The maintainers will review it as soon as possible.

Thank you for your contribution!