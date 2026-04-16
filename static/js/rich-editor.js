(function () {
  if (!window.tinymce) return;

  var editorSelector = 'textarea.js-rich-editor';
  if (!document.querySelector(editorSelector)) return;

  if (window.tinymce.editors && window.tinymce.editors.length) {
    window.tinymce.remove(editorSelector);
  }

  window.tinymce.init({
    selector: editorSelector,
    menubar: false,
    branding: false,
    height: 420,
    language: 'pt_BR',
    plugins: 'advlist autolink lists link image charmap preview searchreplace visualblocks code fullscreen insertdatetime media table wordcount',
    toolbar: 'undo redo | blocks | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | removeformat code preview',
    content_style: 'body { font-family: Outfit, Arial, sans-serif; font-size:14px }'
  });
})();
