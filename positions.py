# 包含了QQ聊天窗口的各个元素的坐标信息，包括聊天列表、聊天窗口、发送按钮、评论区、退出按钮、发送图片按钮等。

DEFAULT_SIZE=(2240,1260)
DEFAULT_SIZE2=(1280,720)
# chatListBBoxAbsoluteSize=(362,221,362+32,221+594)
chatListBBoxAbsoluteSize=(105,154,105+305,154+1055)
conversationBBoxAbsoluteSize=(421,163,421+1796,163+734)
sendButtonBBoxAbsoluteSize=(2023,1167,2023+182,1167+79)
commentSectionBBoxAbsoluteSize=(563,963,563+1455,963+271)
exitConversationBBoxAbsoluteSize=(367,228,367+31,228+33)
sendImageBBoxAbsoluteSize=(663,917,663+44,917+44)
copyButtonBBoxAbsoluteSize=(1698,1028,1698+52,1028+45)
atPlaceBBoxAbsoluteSize=(108,160,108+165,180+1099)  
uploadImagePossibleBBoxAbsoluteSize=(546,885,546+784,885+188)




startDraggingAbsolutePosition=(1898,882)
endDraggingAbsolutePosition=(435,0)
cancelButtonAbsolutePosition=(1325,697)

#DEFAULT_SIZE2
contactButtonAbsolutePosition=(28,104)
chatButtonAbsolutePosition=(27, 63)


CHAT_LIST_BBOX_RELATIVE_SIZE=(chatListBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],chatListBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],chatListBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],chatListBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
CONVERSATION_BBOX_RELATIVE_SIZE=(conversationBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],conversationBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],conversationBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],conversationBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
SEND_BUTTON_BBOX_RELATIVE_SIZE: tuple[float, float, float, float]=(sendButtonBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],sendButtonBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],sendButtonBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],sendButtonBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
COMMENT_SECTION_BBOX_RELATIVE_SIZE=(commentSectionBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],commentSectionBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],commentSectionBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],commentSectionBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
EXIT_CONVERSATION_BBOX_RELATIVE_SIZE=(exitConversationBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],exitConversationBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],exitConversationBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],exitConversationBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
SEND_IMAGE_BBOX_RELATIVE_SIZE=(sendImageBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],sendImageBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],sendImageBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],sendImageBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
COPY_BUTTON_BBOX_RELATIVE_SIZE=(copyButtonBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],copyButtonBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],copyButtonBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],copyButtonBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
AT_PLACE_BBOX_RELATIVE_SIZE=(atPlaceBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],atPlaceBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],atPlaceBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],atPlaceBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])
UPLOAD_IMAGE_POSSIBLE_BBOX_RELATIVE_SIZE=(uploadImagePossibleBBoxAbsoluteSize[0]/DEFAULT_SIZE[0],uploadImagePossibleBBoxAbsoluteSize[1]/DEFAULT_SIZE[1],uploadImagePossibleBBoxAbsoluteSize[2]/DEFAULT_SIZE[0],uploadImagePossibleBBoxAbsoluteSize[3]/DEFAULT_SIZE[1])



START_DRAGGING_RELATIVE_POSITION=(startDraggingAbsolutePosition[0]/DEFAULT_SIZE[0],startDraggingAbsolutePosition[1]/DEFAULT_SIZE[1])
END_DRAGGING_RELATIVE_POSITION=(endDraggingAbsolutePosition[0]/DEFAULT_SIZE[0],endDraggingAbsolutePosition[1]/DEFAULT_SIZE[1])
CANCEL_BUTTON_RELATIVE_POSITION=(cancelButtonAbsolutePosition[0]/DEFAULT_SIZE[0],cancelButtonAbsolutePosition[1]/DEFAULT_SIZE[1])


CONTACT_BUTTON_RELATIVE_POSITION=(contactButtonAbsolutePosition[0]/DEFAULT_SIZE2[0],contactButtonAbsolutePosition[1]/DEFAULT_SIZE2[1])
CHAT_BUTTON_RELATIVE_POSITION=(chatButtonAbsolutePosition[0]/DEFAULT_SIZE2[0],chatButtonAbsolutePosition[1]/DEFAULT_SIZE2[1])



import logging
logging.debug("chatListBBoxRelativeSize: "+str(CHAT_LIST_BBOX_RELATIVE_SIZE))
logging.debug("conversationBBoxRelativeSize: "+str(CONVERSATION_BBOX_RELATIVE_SIZE))
logging.debug("sendButtonBBoxRelativeSize: "+str(SEND_BUTTON_BBOX_RELATIVE_SIZE))
logging.debug("commentSectionBBoxRelativeSize: "+str(COMMENT_SECTION_BBOX_RELATIVE_SIZE))
logging.debug("exitConversationBBoxRelativeSize: "+str(EXIT_CONVERSATION_BBOX_RELATIVE_SIZE))
logging.debug("sendImageBBoxRelativeSize: "+str(SEND_IMAGE_BBOX_RELATIVE_SIZE))
logging.debug("copyButtonBBoxRelativeSize: "+str(COPY_BUTTON_BBOX_RELATIVE_SIZE))






def toActualSize(relativeSize: tuple[float, float, float, float],size: tuple[int, int]):
    return (int(relativeSize[0]*size[0]),int(relativeSize[1]*size[1]),int(relativeSize[2]*size[0]),int(relativeSize[3]*size[1]))
def toActualPoint(relativePoint: tuple[float, float],size: tuple[int, int]):
    return (int(relativePoint[0]*size[0]),int(relativePoint[1]*size[1]))
