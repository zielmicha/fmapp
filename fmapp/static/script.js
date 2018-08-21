
for (var elem of document.querySelectorAll(".clickable-row")) {
    (function(elem) {
        elem.addEventListener('click', function() {
            elem.querySelector('a').click();
        });
    })(elem);
}

function makeDirBrowser(elem) {
    var inputField = elem.querySelector('[type=text]');
    inputField.type = 'hidden'
    var iframe = document.createElement('iframe')

    iframe.src = '/dir-browser' + (inputField.value || '/');
    iframe.onload = function() {
        var path = iframe.contentWindow.document.body.dataset.path;
        console.log("new path", path);
        inputField.value = path;
    };

    elem.appendChild(iframe);
}

for (var elem of document.querySelectorAll('.dir-browser')) {
    makeDirBrowser(elem);
}

function queueTableRow(row) {
    console.log(row)
    var nameField = row.querySelector('[name=name]')
    var targetPath = row.querySelector('[name=target_path]')
    var targetDir = row.querySelector('.target-dir')

    function updateTargetPath() {
        targetPath.value = targetDir.innerText + nameField.value;
    }
    var dialog = row.querySelector('.target-dir-dialog');

    row.querySelector('.target-dir-change').addEventListener('click', function() {
        row.querySelector('.target-dir-dialog').style.display = 'block';
    })

    dialog.querySelector('button').addEventListener('click', function() {
        dialog.style.display = 'none';
        targetDir.innerText = dialog.querySelector('[name=change-to]').value;
    })

    row.querySelector('.approve-form').addEventListener('submit', updateTargetPath)
}

var queueTable = document.querySelector('#queue-table');
if (queueTable) {
    for (var row of queueTable.querySelectorAll('tr.file')) {
        queueTableRow(row);
    }
}
