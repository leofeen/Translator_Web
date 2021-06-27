const getLineHeight = (jQueryElement) => {
    let lineHeight = jQueryElement.css('line-height');
    let calculatedLineHeight;

    if (lineHeight == 'normal') {
        calculatedLineHeight = parseFloat(jQueryElement.css('font-size').replace('px', '')) * 1.2;
    } else if (lineHeight.indexOf('px') != -1) {
        calculatedLineHeight = parseFloat(lineHeight.replace('px', ''));
    } else if (lineHeight.indexOf('%') != -1) {
        calculatedLineHeight = parseFloat(jQueryElement.css('font-size').replace('px', '')) * parseFloat(lineHeight.replace('%', '')) / 100;
    } else if (lineHeight.indexOf('em') != -1) {
        calculatedLineHeight = parseFloat(jQueryElement.css('font-size').replace('px', '')) * parseFloat(lineHeight.replace('em', ''));
    } else if (lineHeight == 'inheret') {
        calculatedLineHeight = getLineHeight(jQueryElement.parent());
    }

    return calculatedLineHeight;
}