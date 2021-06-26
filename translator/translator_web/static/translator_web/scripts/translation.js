$(document).ready(function() {
    $('.translate-text').on('input', function() {
        const textArea = $('.translate-text');
        const minHeight = parseInt(textArea.css('min-height').slice(0, -2));
        this.style.height = '1px';
        this.style.height = (this.scrollHeight + 3) + 'px';
        if (this.scrollHeight + 3 < minHeight) {
            this.style.height = minHeight + 'px'
        } 
    })

    $('.translate-text').on('keydown', function(event) {
        if (event.code == 'Space' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;

            var $this = $(this);
            var value = $this.val();

            $this.val(value.substring(0, start)
                        + "  "
                        + value.substring(end));

            this.selectionStart = this.selectionEnd = start + 2;
        }
    })

    $('.form-translate').submit(function(event) {
        event.preventDefault();

        const data_string = $(this).serialize();
        const url = event.target.action;

        $.ajax({
            method: 'GET',
            data: data_string,
            url: url,
            success: function(reply_text) {
                $('.code-output').text(reply_text);
            },
        })
    })
})