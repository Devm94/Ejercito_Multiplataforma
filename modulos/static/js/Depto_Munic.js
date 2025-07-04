$(document).ready(function () {
  $('#departamento').change(function () {
    var depto_id = $(this).val();
    var url = $('#departamento').data('url'); // Usamos data-url en el HTML

    if (depto_id) {
      $.ajax({
        url: url,
        data: { depto_id: depto_id },
        success: function (data) {
          $('#municipio').empty();
          $('#municipio').append('<option value="" selected>Selecciona un municipio</option>');
          $.each(data, function (key, value) {
            $('#municipio').append('<option value="' + value.id + '">' + value.descrip_corta + '</option>');
          });
        }
      });
    } else {
      $('#municipio').empty().append('<option value="">Selecciona un modelo</option>');
    }
  });

  $('#municipio').change(function () {
    var municipios_id = $(this).val();
    var url = $('#municipio').data('url');

    if (municipios_id) {
      $.ajax({
        url: url,
        data: { cod_munic: municipios_id },
        success: function (data) {
          $('#cv').empty();
          $('#cv').append('<option value="" selected>Selecciona el centro de votación</option>');
          $.each(data, function (key, value) {
            $('#cv').append('<option value="' + value.id + '">' + value.nom + '</option>');
          });
        }
      });
    } else {
      $('#cv').empty().append('<option value="">Selecciona un modelo</option>');
    }
  });

  $('#cv').change(function () {
    var cv_id = $(this).val();
    var url = $('#cv').data('url');

    if (cv_id) {
      $.ajax({
        url: url,
        data: { cod_cv: cv_id },
        success: function (data) {
          // Puedes procesar datos si necesitas
        }
      });
    } else {
      $('#cv').empty().append('<option value="">Selecciona un centro de votación</option>');
    }
  });
});
