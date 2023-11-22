# Dumps search for ExamTopics
*With free tier, ExamTopic only allows us to see limited questions and answers. This tool is to generate HTML files containing any questions and discussion sessions on ExamTopic.*

# Pre-requiste
- `Python` >= `3.9`

# Supported exams
- Google Cloud Platform - Associate Cloud Engineer (`gcp-ace`)
- Amazon Web Services - Certified Security Specialty (`aws-scs`)
- AWS - SAA-C03 (`saa-c03`)
- Microsoft - AI-900 (`ai-900`)
- AWS - CLF-C02 (`clf-c02`)

# Set up
Set up virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```

# Usage
```
usage: main.py [-h] [--start START] [--end END] [--exam EXAMCODE]

Generate HTMLs for GCP ACE exam questions

optional arguments:
  -h, --help                    show this help message and exit
  --start START                 first question index to query
  --end END                     last question index to query
  --exam EXAMCODE               exam code (See `Supported exams` section above)
```

Example:

- This will generate HTML files from question #1 to question #31 the exam AWS-SCS:

    ```bash
    python3 main.py --start 1 --end 31 --exam aws-scs
    ```