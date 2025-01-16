(function($) {
    'use strict';
    $(document).ready(function() {
        function updateFields() {
            var recurrenceType = $('#id_recurrence_type').val();
            var weekdayField = $('.field-weekday');
            var annualFields = $('.field-annual_month, .field-annual_day');

            // Esconde todos os campos específicos
            weekdayField.hide();
            annualFields.hide();

            // Mostra campos baseado no tipo selecionado
            if (recurrenceType === 'weekly') {
                weekdayField.show();
            } else if (recurrenceType === 'annual') {
                annualFields.show();
            }
        }

        // Atualiza campos quando a página carrega
        updateFields();

        // Atualiza campos quando o tipo de recorrência muda
        $('#id_recurrence_type').change(updateFields);
    });
})(django.jQuery);
