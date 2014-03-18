            $(document).ready(function(){
                $('.mb-date').tooltip()

                console.log('hello world')

                // ------------------------------------------------------------
                // Rank form
                $('#rank-form').hide()
                $('.open-rank-form').click(function() {
                    $('#rank-form').toggle('fast')
                })

                $('.typeahead-rank').typeahead({
                    name: 'ranks',
                    prefetch: '/ranks',
                    remote: '/ranks?q=%QUERY'
                    // local: [ "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune" ]
                });

                // ------------------------------------------------------------
                // Planned MB form
                $('#planned-mb-form').hide()
                $('.open-planned-mb-form').click(function() {
                    $('#planned-mb-form').toggle('fast')
                })

                $('.typeahead-planned-mb').typeahead({
                    name: 'planned-mbs',
                    prefetch: '/meritbadges',
                    remote: '/meritbadges?q=%QUERY'
                });

                // ------------------------------------------------------------
                // Earned MB form
                $('#earned-mb-form').hide()
                $('.open-earned-mb-form').click(function() {
                    $('#earned-mb-form').toggle('fast')
                })

                $('.typeahead-earned-mb').typeahead({
                    name: 'earned-mbs',
                    prefetch: '/meritbadges',
                    remote: '/meritbadges?q=%QUERY'
                });

                // ------------------------------------------------------------
                // Export form
                $('#export-form').hide()
                $('.open-export-form').click(function() {
                    $('#export-form').toggle('fast')
                })

                $('.save-export').click(function() {
                    $('#export-form').toggle('fast')  
                })

                // ------------------------------------------------------------
                // Not sure if this is needed
                $('.tt-dropdown-menu').css('z-index', 999999)

                $('.datepicker').datepicker({
                    format: 'mm/dd/yyyy',
                    autoclose: true
                });

                $('.save-earned-mb').click(function() {
                    console.log(this)
                    scout_id = document.URL.split('/').slice(-1)[0].split('#')[0]
                    var mb_name = $('#earned-mb-name').val()
                    var mb_date = $('#earned-mb-date').val()
                    console.log(mb_name)

                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutmeritbadge',
                        data: {
                            scout_id: scout_id,
                            mb_name: mb_name,
                            mb_date: mb_date,
                            csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                            action: 'add',
                            entry_type: 'earned'
                        },
                        dataType: 'json',
                        success: function(data) {
                            earned_mb_html = '<div class="pull-left mb-card">' +
                                                 '<img src="' + template_vars.static_url + 'img/merit_badges/' + data.image_name + '" width="80" height="80" class="top-margin-small" style="margin: auto; display: block;">' +
                                                 '<div>' +
                                                     '<h6 style="white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">' +
                                                         data.name + '</h6>' +
                                                     '<h6 class="text-muted">' + data.mb_date + '</h6>' +
                                                 '</div>' +
                                                 '<a class="delete-earned-mb earned-mb-delete hand-pointer" id="' + data.scoutmeritbadge_id + '"><i class="icon-minus-sign"></i></a>' +
                                             '</div>'

                            $('#earned-mb-div').append(earned_mb_html)

                            $('#planned-mb-' + data.scoutmeritbadge_id).remove()
                        }
                    })

                    $('#earned-mb-form').toggle('fast')
                    return false
                })

                $('.delete-earned-mb').click(function() {
                    $this_el = $(this)
                    id = $(this).attr('id')
                    console.log($(this).attr('id'))
                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutmeritbadge',
                        data: {scout_merit_badge_id: id,
                               csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                               action: 'delete',
                            entry_type: 'earned'},
                        dataType: 'json',
                        success: function(data) {
                            $this_el.parent().remove()
                        }
                    })
                })

                $('.save-planned-mb').click(function() {
                    console.log(this)
                    scout_id = document.URL.split('/').slice(-1)[0].split('#')[0]
                    var mb_name = $('#planned-mb-name').val()
                    var mb_date = $('#planned-mb-date').val()
                    console.log(mb_name)

                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutmeritbadge',
                        data: {
                            scout_id: scout_id,
                            mb_name: mb_name,
                            mb_date: mb_date,
                            csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                            action: 'add',
                            entry_type: 'planned'
                        },
                        dataType: 'json',
                        success: function(data) {
                            console.log('almost!!!')
                            console.log(data)
                            if (data.created == true) {
                                console.log('success!!!')
                                if (data.book_in_library == 'True') {
                                    if (data.book_date_requested && !data.book_date_borrowed) {
                                        book_status = 'Book requested, you will be contacted soon<br />'
                                    } else if (data.book_date_requested) {
                                        book_status = 'Book checked out (due ' + data.book_date_due + ')<br />'
                                    } else {
                                        book_status = '<a class="request-mbbook" href="#" id="' + data.meritbadge_id + '">Check out book</a><br />'
                                    }
                                } else {
                                    book_status = 'Book not in library<br />'
                                }

                                planned_mb_html =   '<div class="row-fluid" id="planned-mb-' + data.scoutmeritbadge_id + '">' +
                                                        '<div class="col-lg-4">' +
                                                            '<img src="' + template_vars.static_url + 'img/merit_badges/' + data.image_name + '" width="80" height="80">' +
                                                            '<a class="delete-planned-mb badge-delete" id="' + data.scoutmeritbadge_id + '"><i class="icon-minus-sign"></i></a>' +
                                                        '</div>' +
                                                        '<div class="col-lg-8">' +
                                                            '<h3 class="compact">' +
                                                                data.name + ' <small>' + data.mb_date + '</small>' +
                                                            '</h3>' +
                                                            book_status +
                                                            '<a class="view-mbcounselors" id="' + data.meritbadge_id + '" href="#">Merit Badge Counselors</a>' +
                                                            '<hr class="dashed-line">' +
                                                        '</div>' +
                                                    '</div>'
                                
                                $('#planned-mb-div').append(planned_mb_html)
                            }
                        }
                    })
                })

                $('.delete-planned-mb').click(function() {
                    $this_el = $(this)
                    id = $(this).attr('id')
                    console.log($(this).attr('id'))
                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutmeritbadge',
                        data: {scout_merit_badge_id: id,
                               csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                               action: 'delete',
                               entry_type: 'planned'},
                        dataType: 'json',
                        success: function(data) {
                            $this_el.parent().parent().remove()
                        }
                    })
                })

                $('.save-rank').click(function() {
                    console.log(this)
                    scout_id = document.URL.split('/').slice(-1)[0].split('#')[0]
                    var rank_name = $('#rank-name').val()
                    var rank_date = $('#rank-date').val()
                    console.log(rank_name)

                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutrank',
                        data: {
                            scout_id: scout_id,
                            rank_name: rank_name,
                            rank_date: rank_date,
                            csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                            action: 'add'
                        },
                        dataType: 'json',
                        success: function(data) {
                            console.log(data)
                            earned_rank_html = 
                                        '<td id="scout-rank-' + data.rank_id + '">' +
                                            '<img src="' + template_vars.static_url + 'img/ranks/' + data.image_name + '" width="100%">' +
                                            '<a class="delete-rank rank-delete hand-pointer" id="' + data.scoutrank_id + '"><i class="icon-minus-sign"></i></a>' +
                                            '<h3 class="text-center rank-label">' +
                                                data.name +
                                            '</h3>' +
                                            '<p class="text-center text-muted rank-label">' +
                                                data.rank_date +
                                            '</p>' +
                                        '</td>'

                            $('#scout-rank-' + data.rank_id).replaceWith(earned_rank_html)
                        }
                    })

                    $('#rank-form').toggle('fast')
                    return false
                })

                $('.delete-rank').click(function() {
                    $this_el = $(this)
                    id = $(this).attr('id')
                    console.log($(this).attr('id'))
                    $.ajax({
                        type: 'POST',
                        url: '/update-scoutrank',
                        data: {scout_rank_id: id,
                               csrfmiddlewaretoken: $(template_vars.csrf_token).val(),
                               action: 'delete'},
                        dataType: 'json',
                        success: function(data) {
                            $('#scout-rank-' + id).replaceWith('<td id="scout-rank-' + data.rank_id + '"><img src="' + template_vars.static_url + 'img/ranks/' + data.image_ph_name + '" width="100%"></td>')
                        }
                    })
                })

                $('.request-mbbook').click(function() {
                    $this_el = $(this)
                    id = $this_el.attr('id')
                    console.log('here0')
                    $.ajax({
                        type: 'POST',
                        url: '/request-mbbook',
                        data: {meritbadge_id: id,
                               csrfmiddlewaretoken: $(template_vars.csrf_token).val()},
                        dataType: 'json',
                        success: function(data) {
                            console.log('here')
                            $this_el.replaceWith(data.outcome)
                        }
                    })
                })

                $('.view-mbcounselors').click(function() {
                    console.log('hi there')
                    $this_el = $(this)
                    id = $this_el.attr('id')
                    console.log('hi there')
                    $('#mbcounselors-modal').modal({remote: '/view-mbcounselors/' + id})
                })

            });
