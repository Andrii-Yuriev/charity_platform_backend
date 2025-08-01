function customizeAdmin() {
    const sidebarDashboardLink = document.querySelector('.nav-sidebar a[href="/admin/"] p');
    if (sidebarDashboardLink && sidebarDashboardLink.textContent.trim() === 'Dashboard') {
        sidebarDashboardLink.textContent = 'Головна панель';
    }

    const mainHeader = document.querySelector('h1.m-0');
    if (mainHeader && mainHeader.textContent.trim() === 'Dashboard') {
        mainHeader.textContent = 'Головна панель';
    }

    const breadcrumbItems = document.querySelectorAll('.breadcrumb-item');
    breadcrumbItems.forEach(function(item) {
        if (item.textContent.trim() === 'Dashboard') {
            item.textContent = 'Головна панель';
        }
    });

    const userAddMessage = document.querySelector('#content-main p');
    if (userAddMessage && userAddMessage.textContent.includes("First, enter a username and password")) {
        userAddMessage.textContent = 'Спочатку введіть адресу електронної пошти та пароль. Після цього ви зможете редагувати інші налаштування автора.';
    }
}


window.addEventListener('load', function() {
    setTimeout(customizeAdmin, 100); 
});

setInterval(customizeAdmin, 300);