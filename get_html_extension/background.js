let isGenerating = false;

browser.action.onClicked.addListener(async (tab) => {
    console.log("Klick!");

    if (isGenerating) {
        console.log("Mail generating is in progress.");
        return;
    }

    isGenerating = true;

    try {
        let content_response;

        try {
            content_response = await browser.tabs.sendMessage(
                tab.id,
                {
                    action: "getHtml"
                }
            );

            console.log("HTML sent");
        } catch (error) {
            console.error("Unable to retrieve HTML from this page. ERROR:", error);
            browser.notifications.create({
                type: "basic",
                title: "Błąd działania rozszerzenia Mail Generator",
                message: "Brak możliwości pobrania danych z tej strony internetowej"
            });
            return;
        }

        const response = await browser.runtime.sendNativeMessage(
            "mail_generator",
            {
                message: content_response.html
            }
        );

        if (!response.ok) {
            console.error(
                `STAGE ERROR ${response.stage}: ${response.error}`
            );
            
            browser.notifications.create({
                type: "basic",
                title: "Błąd działania rozszerzenia Mail Generator",
                message: "Nie udało się poprawnie wygenerować wiadomości"
            });
        }

        console.log("Python response:", response);

    } catch (error) {
        console.error(
            "NATIVE MESSAGING COMMUNICATION ERROR:", error
        );

        browser.notifications.create({
            type: "basic",
            title: "Błąd działania rozszerzenia Mail Generator",
            message: "Nie udało się połączyć z lokalną aplikacją"
        });
    } finally {
        isGenerating = false;
    }
});
