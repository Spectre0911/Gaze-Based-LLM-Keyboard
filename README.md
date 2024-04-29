### Environment Setup

Requires a Python virtual environment and a `.env` configuration file specifying the `OPENAI_API_KEY` key.

#### Quickstart - using venv

> **_NOTE:_** In the venv, use myenv/bin/python and myenv/bin/pip to invoke python and pip respectively.

```bash
# configure the virtual environment
python -m venv myenv
source myenv/bin/activate
myenv/bin/pip install -r requirements.txt

# set the OPENAI_API_KEY
echo "OPENAI_API_KEY=<your-api-key-here>" > .env

# entrypoint is app.py
myenv/bin/python app.py
```
