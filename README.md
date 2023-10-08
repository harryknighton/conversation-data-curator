# Conversation Data Curator

## Set up
This application uses the [pdm](https://github.com/pdm-project/pdm) package manager.
To set up the environment given in pyproject.toml, use
```pdm install```.

## Usage


## License
There is currently no license to use, modify or distribute this work.
All rights belong to the author.

## Repository Overview and Design Justification
### Software Engineering Methodology
CI using GitHub workflows
Pre-commit using flake8, black, isort and mypy.
one commit per PR by interactive rebase or squash merge with small PRs and adequate decomposition.
Detailed PRs and commit names leave a good code history.


milestone per user story
individual issues managed using a GitHub project.

### Data Model

### Web Interface
TBC

## Other Considerations
### Pitfalls of this approach

### Using this software to train and evaluate a classifier to automatically code messages

### Future additions required for demonstrable and responsible AI
Metadata
Bias analysis (representation)
Data Drift

[Training-serving skew](https://www.qwak.com/post/training-serving-skew-in-machine-learning)

Disclosures
    Explicit about limitations of the model
    Notices about data
    Data privacy

Feedback monitoring and live analysis
    Detect distribution drift
