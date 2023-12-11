@implementation StatusManager

- (void) hideVPN:(bool)hidden {
    [self.setter hideVPN:hidden];
}

- (bool) isMicrophoneUseHidden {
    return [self.setter isMicrophoneUseHidden];
}

- (void)hideMicrophoneUse:(bool)hidden withVolume:(float)volume {}

- (bool) isCameraUseHidden {
    return [self.setter isCameraUseHidden];
}

- (void) hideCameraUse:(bool)hidden {
    [self.setter hideCameraUse:hidden];
}

- (bool)hasStyleOverrides:(StatusManagerStyle)style {
    return [self.setter getStyleOverrides] & style;
}

- (void)addStyleOverrides:(StatusManagerStyle)style {
    [self.setter addStyleOverrides:style];
}

- (void)removeStyleOverrides:(StatusManagerStyle)style {
    [self.setter removeStyleOverrides:style];
}

@end