DEFAULT_SIZE=(2240,1260)
# chatListBBoxAbsoluteSize=(362,221,362+32,221+594)
chatListBBoxAbsoluteSize=(105,154,105+305,154+1055)
conversationBBoxAbsoluteSize=(421,163,421+1796,163+734)
sendButtonBBoxAbsoluteSize=(2023,1167,2023+182,1167+79)
commentSectionBBoxAbsoluteSize=(563,963,563+1455,963+271)
exitConversationBBoxAbsoluteSize=(367,228,367+31,228+33)
CHAT_LIST_BBOX_RELATIVE_SIZE=(chatListBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],chatListBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],chatListBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],chatListBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
CONVERSATION_BBOX_RELATIVE_SIZE=(conversationBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],conversationBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],conversationBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],conversationBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
SEND_BUTTON_BBOX_RELATIVE_SIZE: tuple[float, float, float, float]=(sendButtonBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],sendButtonBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],sendButtonBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],sendButtonBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
COMMENT_SECTION_BBOX_RELATIVE_SIZE=(commentSectionBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],commentSectionBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],commentSectionBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],commentSectionBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
EXIT_CONVERSATION_BBOX_RELATIVE_SIZE=(exitConversationBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],exitConversationBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],exitConversationBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],exitConversationBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])

import logging
logging.info("chatListBBoxRelativeSize: "+str(CHAT_LIST_BBOX_RELATIVE_SIZE))
logging.info("conversationBBoxRelativeSize: "+str(CONVERSATION_BBOX_RELATIVE_SIZE))
logging.info("sendButtonBBoxRelativeSize: "+str(SEND_BUTTON_BBOX_RELATIVE_SIZE))
logging.info("commentSectionBBoxRelativeSize: "+str(COMMENT_SECTION_BBOX_RELATIVE_SIZE))


def toActualSize(relativeSize: tuple[float, float, float, float],size: tuple[int, int]):
    return (int(relativeSize[0]*size[0]),int(relativeSize[1]*size[1]),int(relativeSize[2]*size[0]),int(relativeSize[3]*size[1]))
