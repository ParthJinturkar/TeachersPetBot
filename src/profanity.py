from better_profanity import profanity

profanity.load_censor_words()


###########################
# Function: check_profanity
# Description: Uses better_profanity to check profanity in a message
# Inputs:
#      - msg: message from user
###########################
def check_profanity(msg):
    """
    Function:
        check_profanity
    Description:
        Uses 'contains_profanity' to check profanity of a message
    Input:
        - msg: message from user
    Output:
        None
    """
    ''' check if message contains profanity through profanity module '''
    return profanity.contains_profanity(msg)


###########################
# Function: censor_profanity
# Description: censor the message per better_profanity
# Inputs:
#      - msg: message from user
###########################
def censor_profanity(msg):
    """
    Function:
        censor_profanity
    Description:
        censors a message based on profanity
    Input:
        - msg: message from user
    Output:
        None
    """
    return profanity.censor(msg)
