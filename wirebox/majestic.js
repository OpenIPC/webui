const from1to99 = Array.from({length: 98}, (_, i) => i + 1);
const from1to500k = Array.from({length: 499999}, (_, i) => i + 1);

const majectic = {
    system: {
        logLevel: {
            default: 'WARN',
            description: 'Severity of logging.',
            values: ['ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE'],
        },
        sensorConfig: {
            default: '/etc/sensors/imx222_1080p_line.ini',
            description: 'Path to sensor configuration file.',
            hint: 'If not set, SENSOR environment variable will be used.',
        },
        sensorConfigDir: {
            default: '/etc/sensors',
            description: 'Path to sensor configs directory.',
        },
        webPort: {
            default: 80,
            description: 'Port for HTTP access.',
            hint: 'Usually, port 80.',
        },
        staticDir: {
            default: '/var/www/html',
            description: 'Home directory for static files.',
        },
        httpsPort: {
            default: 443,
            description: 'Port for HTTPS access.',
            hint: 'Usually, port 443.',
        },
        httpsCertificate: {
            default: '/etc/ssl/certs/www.example.com.crt',
            description: 'Path to public SSL certificate.',
        },
        httpsCertificateKey: {
            default: '/etc/ssl/private/www.example.com.key',
            description: 'Path to private SSL key.',
        },
        updateChannel: {
            default: 'stable',
            description: 'Channel to use for updates.',
            values: ['testing', 'beta', 'stable', 'none'],
        },
        buffer: {
            default: 1024,
            description: 'Maximum buffer size per client.',
            units: 'KB',
        },
    },
    isp: {
        memMode: {
            default: 'reduction',
            description: 'Memory mode.',
            values: ['normal', 'reduction'],
        },
        slowShutter: {
            default: 'low',
            description: 'Automatic frame rate reduction mode (slow shutter mode).',
            values: ['disabled', 'low', 'medium', 'high'],
        },
        antiFlicker: {
            default: 'disabled',
            description: 'Utility frequency in your power line.',
            units: 'Hz',
            values: [50, 60, 'disabled'],
        },
        alignWidth: {
            default: 8,
        },
        blkCnt: {
            default: 4,
            description: 'Use 4 for small memory systems, 10+ for performant SoCs.',
        },
        threadStackSize: {
            default: 16,
            units: 'KB',
        },
        exposure: {
            default: 'auto',
            description: 'Exposition time. from 1 to 500000 or auto',
            units: 'ms',
            values: [from1to500k, 'auto'],
        },
        aGain: {
            default: 1,
        },
        dGain: {
            default: 1,
        },
        ispGain: {
            default: 1,
        },
        drc: {
            default: 300,
            units: ':1',
            description: 'Dynamic Range Compression rate.',
        },
    },
    image: {
        mirror: {
            default: false,
            description: 'Flip image horizontally.',
            values: [true, false],
        },
        flip: {
            default: false,
            description: 'Flip image vertically.',
            values: [true, false],
        },
        rotate: {
            default: 'none',
            description: 'Rotate image clockwise.',
            units: '⁰',
            values: ['none', 90, 270],
        },
        contrast: {
            default: 'auto',
            description: 'Image contrast.',
            values: ['auto', from1to99],
        },
        hue: {
            default: 50,
            description: 'Image hue.',
            values: from1to99,
        },
        saturation: {
            default: 50,
            description: 'Image saturation.',
            values: from1to99,
        },
        luminance: {
            default: 'auto',
            description: 'Image luminance.',
            values: ['auto', from1to99],
        },
    },
    osd: {
        enabled: {
            default: false,
            description: 'Enable On-Screen Display (OSD).',
            values: [true, false],
        },
        font: {
            description: 'Path to font file ti use for OSD.',
            default: '/usr/lib/fonts/fonts.bin',
        },
        template: {
            default: "%a %e %B %Y %H:%M:%S %Z",
            description: 'OSD template, supports strftime() format.',
            hint: 'Use %f to show milliseconds (consumes more resources).',
        },
        posX: {
            default: -100,
            description: 'Horizontal position of OSD.',
            hint: 'Positive values count from left/top, negative - from right/bottom',
            units: 'px',
        },
        posY: {
            default: -100,
            description: 'Vertical position of OSD.',
            hint: 'Positive values count from left/top, negative - from right/bottom',
            units: 'px',
        },
        privacyMasks: {
            default: '0x0x234x640,2124x0x468x1300',
            hint: 'Coordinates of masked areas separated by commas.',
            units: 'px',
        },
    },
    nightMode: {
        enabled: {
            default: false,
            description: 'Enable night mode.',
            values: [true, false],
        },
        irSensorPin: {
            default: 62,
            description: 'GPIO pin of signal from IR sensor.',
        },
        irSensorPinInvert: {
            default: false,
            description: 'IR sensor is inverted.',
            values: [true, false],
        },
        irCutPin1: {
            default: 1,
            description: 'GPIO pin1 of signal for IRcut filter.',
        },
        irCutPin2: {
            default: 2,
            description: 'GPIO pin2 of signal for IRcut filter.',
        },
        pinSwitchDelayUs: {
            default: 150,
            description: 'Delay before triggering IRcut filter.',
            hint: 'WARNING! A very long delay can damage the IRcut filter!',
            units: 'μs',
        },
        backlightPin: {
            default: 65,
            description: 'GPIO pin to turn on backlight illumination in night mode.',
        },
        nightAPI: {
            default: false,
            description: 'Use night mode API.',
            hint: 'Use /night/{invert,on,off} endpoints to change mode by API for remote callers.',
            values: [true, false],
        },
        drcOverride: {
            default: 300,
            description: 'DRC in night mode.',
        },
    },
    records: {
        enabled: {
            default: false,
            description: 'Enable saving records.',
            values: [true, false],
        },
        path: {
            default: '/mnt/mmc/%Y/%m/%d/%H.mp4',
            description: 'Template for saving video records. Supports strftime() format.'
        },
        maxUsage: {
            default: 95,
            description: 'Limit of available space usage.',
            units: '%',
        },
    },
    video0: {
        enabled: {
            default: true,
            description: 'Enable Video0.',
            values: [true, false],
        },
        codec: {
            default: 'h264',
            description: 'Video0 codec.',
            values: ['h264', 'h265'],
        },
        size: {
            default: '1920x1080',
            description: 'Video resolution.',
            hint: 'Usually 1920x1080, 1280x720, or 704x576.',
            units: 'px',
        },
        fps: {
            default: 25,
            description: 'Video frame rate.',
            units: 'frames',
        },
        bitrate: {
            default: '4096',
            description: 'Video bitrate.',
            units: 'kbps',
        },
        gopSize: {
            default: 1,
            description: 'Send I-frame each 1 second.',
        },
        gopMode: {
            default: 'normal',
            description: 'GOP mode.',
            values: ['normal', 'dual', 'smart'],
        },
        rcMode: {
            default: 'avbr',
            description: 'RC mode.',
        },
        crop: {
            default: '0x0x960x540',
            description: 'Crop video to size.',
            units: 'px',
        },
    },
    video1: {
        enabled: {
            default: true,
            description: 'Enable Video1.',
            values: [true, false],
        },
        codec: {
            default: 'h264',
            description: 'Video1 codec.',
            values: ['h264', 'h265'],
        },
        size: {
            default: '1920x1080',
            description: 'Video resolution.',
            hint: 'Usually 1920x1080, 1280x720, or 704x576.',
            units: 'px',
        },
        fps: {
            default: 25,
            description: 'Video frame rate.',
            units: 'frames',
        },
        bitrate: {
            default: 4096,
            description: 'Video bitrate.',
            units: 'kbps',
        },
        gopSize: {
            default: 1,
            description: 'send I-frame each 1 second',
        },
        gopMode: {
            default: 'normal',
            values: ['normal', 'dual', 'smart'],
        },
        rcMode: {
            default: 'avbr',
        },
        crop: {
            default: '0x0x960x540',
            description: 'Crop video to size.',
            units: 'px',
        }
    },
    jpeg: {
        enabled: {
            default: true,
            description: 'Enable JPEG support.',
            values: [true, false],
        },
        size: {
            default: '1920x1080',
            description: 'Snapshot size.',
            units: 'px',
        },
        qfactor: {
            default: 50,
            description: 'JPEG quality level.',
            units: '%',
            values: from1to99,
        },
        toProgressive: {
            default: false,
            description: 'Transform to Progressive JPEG.',
            values: [true, false],
        },
    },
    mjpeg: {
        size: {
            default: '640x360',
            description: 'Video resolution.',
            units: 'px',
        },
        fps: {
            default: 5,
            description: 'Video framerate.',
            units: 'frames',
        },
        bitrate: {
            default: 1024,
            description: 'Video bitrate.',
            units: 'kbps',
        },
    },
    audio: {
        enabled: {
            default: false,
            description: 'Enable audio.',
            values: [true, false],
        },
        volume: {
            default: 'auto',
            description: 'Audio volume level.',
            units: '%',
            values: ['auto', from1to99],
        },
        srate: {
            default: 8000,
            description: 'Audio sampling rate.',
            units: 'Hz',
        },
        codec: {
            default: 'opus',
            description: 'Codec for RTSP and MP4 encoding.',
            values: ['mp3', 'opus', 'aac', 'pcm'],
        },
        device: {
            default: 'hw:3',
            description: 'Audio card.',
            hint: 'Run `arecord -l` to find card ID.',
        },
        outputEnabled: {
            default: false,
            description: 'Enable output.',
            values: [true, false],
        },
    },
    rtsp: {
        enabled: {
            default: true,
            description: 'Enable Real Time Streaming Protocol (RTSP).',
            values: [true, false],
        },
        port: {
            default: 554,
            description: 'RTSP port.',
            hint: 'Usually, it is a port 554.'
        },
    },
    hls: {
        enabled: {
            default: true,
            description: 'Enable HTTP Live Streaming (HLS).',
            values: [true, false],
        },
    },
    youtube: {
        enabled: {
            default: false,
            description: 'Enable Youtube support.',
            values: [true, false],
        },
        key: {
            default: '',
            description: 'Youtube API key.',
            format: 'xxxx-xxxx-xxxx-xxxx-xxxx',
        }
    },
    motionDetect: {
        enabled: {
            default: false,
            description: 'Enable motion detection.',
            values: [true, false],
        },
        profile: {
            default: 'outdoor',
            description: 'Motion detection profile to use.',
            values: ['outdoor', 'indoor'],
        },
        visualize: {
            default: true,
            description: 'Visualize motion detection.',
            values: [true, false],
        },
        debug: {
            default: true,
            description: 'Enable debugging.',
            values: [true, false],
        },
        constraints: {
            default: '0x0x1296x760',
            description: 'Regions of Interest (ROI) for motion detection.',
            hint: 'Region coordinates separated by commas.',
            units: 'px',
        }
    },
    ipeye: {
        enabled: {
            default: false,
            description: 'Enable IP EYE support.',
            values: [true, false],
        },
    },
    netip: {
        enabled: {
            default: false,
            description: 'Enable NETIP protocol support.',
            values: [true, false],
        },
        user: {
            default: 'admin',
            description: 'NETIP user.',
        },
        password: {
            default: '6V0Y4HLF',
            description: 'NETIP password.',
        },
        port: {
            default: 34567,
            description: 'NETIP port.',
        },
        snapshots: {
            default: true,
            description: 'NETIP snaphots.',
            values: [true, false],
        },
        ignore_set_time: {
            default: false,
            description: 'Ignore set time.',
            values: [true, false],
        },
    },
    onvif: {
        enabled: {
            default: false,
            description: 'Enable ONVIF protocol support.',
            values: [true, false],
        },
    },
    raw: {
        enabled: {
            default: false,
            description: 'Enable raw feed support.',
            values: [true, false],
        },
        mode: {
            default: 'slow',
            description: 'Raw feed mode.',
            hint: 'slow: 1 snapshot at a time, fast: series of snapshots, none: disabled',
            values: ['slow', 'fast', 'disabled'],
        },
    },
    watchdog: {
        enabled: {
            default: false,
            description: 'Enable watchdog support.',
            values: [true, false],
        },
        timeout: {
            default: 10,
            description: 'Watchdog timeout.',
            units: 'ms',
        },
    },
    cloud: {
        enabled: {
            default: false,
            description: 'Enable cloud support.',
            values: [true, false],
        },
    },
}
