FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

WORKDIR /template

COPY . /template

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/PocJSONProcessor_2.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="/template/setup.py"

#RUN pip install --no-cache-dir -r /template/requirements.txt

RUN pip install -e .

