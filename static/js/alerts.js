function show_alert(message_tags, message) {
    let alert_type, icon;
    if (message_tags === "error") {
        // If the message is an error, add the error class to the alert
        alert_type = "danger";
        icon = "exclamation-triangle-fill";
    } else if (message_tags === "warning") {
        // If the message is a warning, add the warning class to the alert
        alert_type = "warning";
        icon = "exclamation-triangle-fill";
    } else if (message_tags === "success") {
        // If the message is a success, add the success class to the alert
        alert_type = "success";
        icon = "check-circle-fill";
    } else if (message_tags === "info") {
        // If the message is an info, add the info class to the alert
        alert_type = "primary";
        icon = "info-circle-fill";
    } else {
        // If the message is not one of the above, add the primary class to the alert
        alert_type = "primary";
        icon = "info-circle-fill";
    }
    // Create the alert
    let alert = $("<error class='alert alert-" + alert_type + " alert-dismissible fade show d-flex justify-content-center'" + "role='alert' data-filter-title='" + message_tags + "'>");

    // Add the icon
    alert.append("<i class='bi bi-" + icon + " me-2 flex-shrink-0'></i>");

    // Add the alert message
    alert.append("<div>" + message + "</div>");

    // Add the close button
    alert.append("<button type='button' class='btn-close' data-bs-dismiss='alert'></button>");

    // Add the alert to the DOM
    $("#alerts").append(alert);
}
