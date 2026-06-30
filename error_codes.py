ERR_INVALID_AMOUNT = "INVALID_AMOUNT"
ERR_INVALID_DESCRIPTION = "INVALID_DESCRIPTION"
ERR_INVALID_DATE = "INVALID_DATE"
ERR_INVALID_MONTH = "INVALID_MONTH"
ERR_INVALID_ID = "INVALID_ID"
ERR_ID_DNE = "ID_DOESNT_EXIST"
ERR_FILE_NOT_FOUND = "FILE_NOT_FOUND"
ERR_FILE_MALFORMED = "FILE_MALFORMED"
ERR_NO_UPDATE = "NO_UPDATE"
            

ERROR_MESSAGES = {
    ERR_INVALID_AMOUNT: "Error: The expense amount is invalid.",
    ERR_INVALID_DESCRIPTION: "Error: The description is invalid.",
    ERR_INVALID_DATE: "Error: The date is invalid.",
    ERR_INVALID_MONTH: "Error: The month is invalid.",
    ERR_INVALID_ID: "Error: The ID is invalid.",
    ERR_ID_DNE: "Error: The ID doesn't exist.",
    ERR_FILE_NOT_FOUND: "Error: The file couldn't be found.",
    ERR_FILE_MALFORMED: "Error: File is malformed (incorrect data type/format or headers are missing).",
    ERR_NO_UPDATE: "Error: The ID is present but no update was made."
}

def get_error_message(code: str) -> str:
    """Retrieve the centralized error message."""
    return ERROR_MESSAGES.get(code, "An unknown error occurred.")