import hashlib

def compute_hash(filepath):
    """
    Reads a file and computes its SHA-256 hash.
    This hash is like a fingerprint of the document.
    If even ONE character changes, the hash changes completely.
    """
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:  # rb = read binary (works for PDFs)
        # Read in chunks (good practice for large files)
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()  # Returns 64-character hex string


def verify_hash(filepath, stored_hash):
    """
    Recomputes hash of file and compares with stored hash.
    Returns True if file is authentic, False if tampered.
    """
    current_hash = compute_hash(filepath)
    return current_hash == stored_hash