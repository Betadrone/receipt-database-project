function deleteNote(noteId)
{
    fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId : noteId})
    }).then((_res) => {
        window.location.href = "/";
    })
}

function deleteReceipt(receiptId)
{
    fetch('/delete-receipt', {
    method: 'POST',
    body: JSON.stringify({ receiptId : receiptId})
    }).then((_res) => {
        window.location.href = "/database";
    })
}