import {FaceDetector, FilesetResolver} from "https://fastly.jsdelivr.net/npm/@mediapipe/tasks-vision@latest";

let face_detector;
let runningMode = "VIDEO";
let last_video_time = -1;  // Used for frame rate computation
let selfie_mode = true;
let webcam_active = false;

// open the webcam if the user clicks on the button to open the modal
// before the face_detector is ready
let open_webcam_on_ready = false;

let video = document.getElementById("webcam");
let canvas = document.getElementById("output_canvas");
let context = canvas.getContext("2d");
let facial_login_modal = document.getElementById("facial-login");
let facial_login_button = document.getElementById("facial-login-button");
let warning_message;

// Enable Selfie Mode when the checkbox is checked
$("#selfie-mode").on('change', function () {
    selfie_mode = $(this).is(':checked');
    // flip the video and canvas horizontally if selfie mode is enabled
    if (selfie_mode) {
        video.classList.add('selfie-mode');
        canvas.classList.add('selfie-mode');
    }
    else {
        video.classList.remove('selfie-mode');
        canvas.classList.remove('selfie-mode');
    }
});

// Initialize the object detector
const initialize_face_detector = async () => {
    const vision = await FilesetResolver.forVisionTasks("https://fastly.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm");
    face_detector = await FaceDetector.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite`,
            delegate: "GPU"
        }, runningMode: runningMode
    });

    if (open_webcam_on_ready) {
        warning_message.close();
        open_modal();
    }
};
initialize_face_detector();

async function open_modal() {
    await bootstrap.Modal.getOrCreateInstance(facial_login_modal).show();
}

// Check if webcam access is supported.
const has_user_media = () => {
    let _a;
    return !!((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia);
};
// If webcam supported, add event listener to button for when user
// wants to activate it.
let video_stream = has_user_media();
if (video_stream) {
    facial_login_modal.addEventListener("show.bs.modal", activate_webcam_stream);
    facial_login_modal.addEventListener("hidden.bs.modal", stop_webcam_stream);
}
else {
    console.warn("getUserMedia() is not supported by your browser");
}

// Show the modal when the button is clicked
facial_login_button.addEventListener("click", () => {
    if (!face_detector) {
        // alert("Face Detector is still loading. Please try again..");
        warning_message = Swal.fire({
            title: 'Warning!',
            text: 'Please wait, The webcam will open soon.',
            icon: 'warning',
            confirmButtonText: 'Close'
        });
        open_webcam_on_ready = true;
    }
    else {
        open_modal();
    }
});

// Enable the live webcam view and start detection.
async function activate_webcam_stream() {
    if (!face_detector) {
        warning_message = Swal.fire({
            title: 'Warning!',
            text: 'Please wait, The webcam will open soon.',
            icon: 'warning',
            confirmButtonText: 'Close'
        });
        return;
    }
    if (!webcam_active) {
        webcam_active = true;

        // Activate the webcam stream
        try {
            const constraints = {video: true};
            video.srcObject = await navigator.mediaDevices.getUserMedia(constraints);
            video.addEventListener("loadeddata", predict_webcam);
        }
        catch (error) {
            console.error(error);
        }
    }
}

async function stop_webcam_stream() {
    if (webcam_active) {
        webcam_active = false;
        // Stop the webcam stream
        window.requestAnimationFrame(() => {
            video.srcObject.getTracks().forEach(track => {
                track.stop();
            });
        });
    }
}

async function predict_webcam() {
    let start_time_ms = performance.now();
    // Detect faces using detectForVideo
    if (video.currentTime !== last_video_time) {
        last_video_time = video.currentTime;
        const detections = face_detector.detectForVideo(video, start_time_ms).detections;
        display_video_detections(detections);
    }
    // Call this function again to keep predicting when the browser is ready
    window.requestAnimationFrame(predict_webcam);
}

/**
 * Draws bounding boxes around detected faces in a video stream.
 * @param {Array} detections - An array of face detection objects.
 */
function display_video_detections(detections) {
    // Set canvas dimensions to match video dimensions
    canvas.width = video.offsetWidth;
    canvas.height = video.offsetHeight;
    const width_ratio = video.offsetWidth / video.videoWidth;
    const height_ratio = video.offsetHeight / video.videoHeight;

    // Clear canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Iterate through detections and draw bounding boxes
    for (let detection of detections) {
        // Draw bounding box
        context.beginPath();
        context.rect(detection.boundingBox.originX * width_ratio, (detection.boundingBox.originY - 30) * height_ratio, (detection.boundingBox.width - 10) * width_ratio, (detection.boundingBox.height + 30) * height_ratio);
        context.lineWidth = 2;
        context.strokeStyle = "white";
        context.stroke();
        context.fillStyle = "transparent";
        context.fill();
        context.closePath();

        window.on_face_detection();
    }
}
