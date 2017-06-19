#
# little helper functions to make some things easier for new commands
#

def give(user_id, text, bot):
    '''construct a message to be sent that mentions a user,
    which is surprisingly complicated with GroupMe'''
    from groupy import Group, attachments
    
    group = Group.list().filter(id=bot.group_id).first
    nickname = group.members().filter(user_id=user_id).first.nickname

    mention = attachments.Mentions([user_id], [[0, len(nickname)+1]]).as_dict()
    message = '@{} {}'.format(nickname, text)

    return (message, mention)
