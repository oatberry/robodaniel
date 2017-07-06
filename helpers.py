#
# little helper functions to make some things easier for new commands
#

from groupy import attachments

def give(user_id, text, group):
    """construct a message to be sent that mentions a user,
    which is surprisingly complicated with GroupMe"""
    
    nickname = group.members().filter(user_id=user_id).first.nickname

    mention = attachments.Mentions([user_id], [[0, len(nickname)+1]]).as_dict()
    message = '@{} {}'.format(nickname, text)

    return (message, mention)
