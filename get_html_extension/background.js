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
        }

        console.log("Python response:", response);

    } catch (error) {
        console.error(
            "NATIVE MESSAGING COMMUNICATION ERROR:",
            error
        );
    } finally {
        isGenerating = false;
        console.log("Mail generating is finished.");
    }
});
