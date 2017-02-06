# ecs-webshare

## Introduction

DellEMC Elastic Cloud Storage (ECS) is a software-defined, cloud-scale, object storage platform that combines the cost advantages of commodity infrastructure with comprehensive protocol support for unstructured (Object and File) workloads.

ECS supports several Object Storage APIs (Amazon S3, OpenStack Swift, Atmos, CAS), but the Amazon S3 API is by the far the most popular.

## Goal

The ECS-WebShare application will demonstrate how to upload a file to ECS (or S3 compatible storage) to share it with an expiring link.

Python is used as the core language.  Flask and Flask-Bootstrap were used to develop a self-signed secure front end.

## How do I use the application?

Bring your ECS (or S3 account) or [create](https://portal.ecstestdrive.com/) one.

1. Install Python (3.5 or later)

2. Install the Python requirements:

    ```pip install -r requirements.txt```

3. Run the application:

    ```python app.py```

4. Open your browser and go to your local URL (https://127.0.0.1:3000)

5. Enter your information and file to upload.

6. Press upload

7.  Use the provided link to download the object for the storage.