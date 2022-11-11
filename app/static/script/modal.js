$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const old_id = button.data('id')
        const old_name = button.data('name')  // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New Company') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (old_id) {
            console.log("if")
            console.log(old_id.id)
            modal.find('.form-control-name').val(old_name);
            modal.find('.form-control-id').val(old_id);
        } else {
            console.log("else")
            modal.find('.form-control-name').val('');
            modal.find('.form-control-id').val('');
        }
    })

    $('#submit-search').click(function () {
        const tID = $('#comp-form-display').attr('taskID');
        console.log($('#search-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url:  '/search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'text': $('#search-modal').find('.form-control').val()
            }),
            
            success: function (res) {
                location.replace('/search_page/' +JSON.stringify(res))
                // $.ajax({
                //     type: "GET",
                //     url: '/search_page/' +JSON.stringify(res[0]),
                //     success: function (result) {
                //       console.log(result);
                      
                //     },
                //   });
                // $.ajax({
                //     type: 'POST',
                //     url:  '/search_page',
                //     contentType: 'application/json;charset=UTF-8',
                //     data: JSON.stringify(res[0]),
                //     success: function (res) {
                //         // console.log(res.response)
                //         // location.replace("./search");
                //     },
                //     error: function () {
                //         console.log('inner Error');
                //     }
                // });
                console.log(res.response)
                // location.replace("./search");
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control-id').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'id': $('#task-modal').find('.form-control-id').val(),
                'name': $('#task-modal').find('.form-control-name').val()
            }),
            
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {

        const state = $(this);
        const tID = state.data('source');
        new_state = "";
        if (state.text() === "Follow") {
            new_state = "Unfollow";
        } else if (state.text() === "Unfollow") {
            new_state = "Follow";

        } 

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});