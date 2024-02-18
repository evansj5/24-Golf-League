check_pip() {
    python -m pip --version &> /dev/null
    return $?
}

if ! check_pip; then
    echo "pip could not be found, attempting to install it..."
    python -m ensurepip
    if [ $? -ne 0 ]; then
        echo "Failed to install pip using ensurepip, attempting manual install..."
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py
        if [ $? -ne 0 ]; then
            echo "Failed to install pip, exiting."
            exit 1
        fi
    fi
    echo "pip installed successfully."
fi

echo "Installing required packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install required packages, exiting."
    exit 1
fi
echo "Required packages installed."
echo "Running sgt sync..."
python sgt_sync.py