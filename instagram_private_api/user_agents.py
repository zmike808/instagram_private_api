from .constants import Constants

xiaomi_device_string = '25/7.1.1; 440dpi; 1080x1920; Xiaomi; MI MAX 2; oxygen; qcom'
samsung_device_string = '26/8.0.0; 560dpi; 1440x2792; samsung; SM-G955F; dream2lte; samsungexynos8895'
huawei_device_string = '26/8.0.0; 480dpi; 1080x2150; HUAWEI; ANE-LX1; HWANE; hi6250'


USER_AGENT_XIAOMI = 'Instagram {} Android ({}; en_US; {})'.format(
    Constants.APP_VERSION,
    xiaomi_device_string,
    Constants.VERSION_CODE,
)
USER_AGENT_SAMSUNG = 'Instagram {} Android ({}; en_US; {})'.format(
    Constants.APP_VERSION,
    samsung_device_string,
    Constants.VERSION_CODE,
)
USER_AGENT_HUAWEI = 'Instagram {} Android ({}; en_US; {})'.format(
    Constants.APP_VERSION,
    huawei_device_string,
    Constants.VERSION_CODE,
)
