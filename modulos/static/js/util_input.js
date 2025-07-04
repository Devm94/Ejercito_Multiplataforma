$(document).ready(function () {
    $('.telefono-mask').mask('0000-0000')
    $('#add-seguridad').click(function () {
        let newRow = `
                      <div class="row g-2 mb-3 seguridad-item">
                          <div class="col-md-3">
                              <select class="form-select" name="grado[]">
                                  <option value="">Seleccione</option>
                                  <option value="SGTO">SGTO</option>
                                  <option value="SBTTE">SBTTE</option>
                                  <option value="TTE">TTE</option>
                                  <option value="CPTN">CPTN</option>
                                  <option value="MY">MY</option>
                                  <option value="TCNEL">TCNEL</option>
                                  <option value="CNEL">CNEL</option>
                              </select>
                          </div>
                          <div class="col-md-5">
                              <input type="text" class="form-control" name="nombre_seguridad[]">
                          </div>
                          <div class="col-md-3">
                              <input type="text" class="form-control telefono-mask" name="telefono_seguridad[]" placeholder="####-####">
                          </div>
                          <div class="col-md-1 d-flex align-items-end">
                              <button type="button" class="btn btn-danger btn-sm remove-seguridad">X</button>
                          </div>
                      </div>`
        $('#seguridad-container').append(newRow)
        $('.telefono-mask').mask('0000-0000')
    })

    $(document).on('click', '.remove-seguridad', function () {
        $(this).closest('.seguridad-item').remove()
    })
})