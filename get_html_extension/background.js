browser.action.onClicked.addListener(async (tab) => {
    console.log("Klick!")
    let content_response;
    try {
        content_response = await browser.tabs.sendMessage(
            tab.id,
            {
                action: "getHtml"
            }
        )
        console.log("HTML sent")
    } catch (error) {
        console.log("Nie można pobrać HTML z tej strony. ERROR: ", error)
    }

    try {
        const response = await browser.runtime.sendNativeMessage(
            "mail_generator",
            {
                message: content_response.html
            }
        );

        if (!response.ok) {
            console.error(
                `BŁĄD ETAPU ${response.stage}: ${response.error}`
            )
        }

        console.log("Odpowiedź Pythona: ", response)
    } catch (error) {
        console.error("BŁĄD KOMUNIKACJI NATIVE MESSAGING: ", error)
    }
});