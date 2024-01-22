# Snapshots and Volumes Management Script

This script provides helper commands for managing AWS Snapshots and Volumes.

## Prerequisites

- Python 3 installed
- Boto3 library installed (you can install it using `pip install boto3`)

## Usage

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the script directory:

    ```bash
    cd path/to/script
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure AWS credentials:

   Ensure your AWS credentials are configured. You can set them up using the AWS CLI:

    ```bash
    aws configure
    ```

5. Run the script:

    ```bash
    ./test.py snapshot_delete
    ```

## Commands

### `snapshot_delete`

Deletes specific snapshots by ID if they are unused.

```bash
./script.py snapshot_delete
