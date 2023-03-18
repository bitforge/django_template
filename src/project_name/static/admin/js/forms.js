$(function() {
    // Init autosize textfields
    autosize($('textarea.autosize'));

    // Init simple markdown editor
    // https://simplemde.com/
    $('.markdown').each(function () {
        new SimpleMDE({
            element: this,
            toolbar: [
                'heading-1', 'heading-2', 'heading-3', '|',
                'bold', 'italic', '|',
                'unordered-list', 'ordered-list', '|',
                'preview'
            ],
            spellChecker: false
        });
    });

    // Loading overlay on form submits
    $('form').submit(function() {
        // Check validity before submit on forms that opted in for this
        if ($('body').hasClass('validate-on-submit')) {
            const is_valid = this.reportValidity();
            if (!is_valid) return false;
        }

        // Prevent showing overlay on forms that opted-out
        if ($(this).hasClass('no-overlay')) {
            return true;
        }

        // Show loading overlay when submitting form / uploading data
        $.LoadingOverlay("show");
        return true;
    });
});
