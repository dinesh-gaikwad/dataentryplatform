def nav_items(active=None):
    items = [
        {"name":"Dashboard","url":"/","icon":"bi-speedometer2","key":"dashboard"},
        {"name":"Records","url":"/records","icon":"bi-journal-text","key":"records"},
        {"name":"Users","url":"/users","icon":"bi-people","key":"users"},
        {"name":"Workflows","url":"/workflows","icon":"bi-diagram-3","key":"workflows"},
        {"name":"Forms","url":"/forms","icon":"bi-ui-checks-grid","key":"forms"},
        {"name":"Imports","url":"/imports","icon":"bi-file-earmark-arrow-up","key":"imports"},
        {"name":"Exports","url":"/exports","icon":"bi-file-earmark-arrow-down","key":"exports"},
        {"name":"Analytics","url":"/analytics","icon":"bi-graph-up","key":"analytics"},
        {"name":"Reports","url":"/reports","icon":"bi-file-earmark-bar-graph","key":"reports"},
        {"name":"Notifications","url":"/notifications","icon":"bi-bell","key":"notifications"},
        {"name":"Logs","url":"/logs","icon":"bi-journal-check","key":"logs"},
        {"name":"Settings","url":"/settings","icon":"bi-gear","key":"settings"},
        {"name":"Help","url":"/help","icon":"bi-question-circle","key":"help"},
        {"name":"Login","url":"/login","icon":"bi-box-arrow-in-right","key":"login"},
        {"name":"Register","url":"/register","icon":"bi-person-plus","key":"register"},
    ]
    for item in items:
        item["active"] = item["key"] == active
    return items
