FROM apache/spark-py:latest

# Install Jupyter Notebook
USER root
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install jupyter

# Set the working directory
WORKDIR /opt/notebooks

# Expose the Jupyter Notebook port
EXPOSE 8888

# Command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/opt/notebooks"]