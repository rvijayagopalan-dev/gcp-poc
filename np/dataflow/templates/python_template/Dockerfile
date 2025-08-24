FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

COPY . /template
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/PocJSONProcessor_1.py"
RUN pip install --no-cache-dir -r /template/requirements.txt