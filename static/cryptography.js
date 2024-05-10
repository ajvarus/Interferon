function enableTextarea() {
  const enumSelector = document.getElementById("enumSelector");
  const plaintext = document.getElementById("plaintextArea");
  const sendButton = document.getElementById("sendButton");

  enumSelector.addEventListener("change", function () {
    const enumSelectorValue = enumSelector.value;
    plaintext.disabled = !enumSelectorValue;
    sendButton.disabled = !enumSelectorValue;
  });
}

function encryptText() {
  const cryptType = "{{ crypt_type.get('display_name') }}".toLowerCase();
  const sendButton = document.getElementById("sendButton");

  sendButton.addEventListener("click", function () {
    const plaintext = document.getElementById("plaintextArea").value;
    const cryptEnumType = document.getElementById("enumSelector").value;

    const data = {
      plaintext: plaintext,
      cryptEnumType: cryptEnumType,
    };

    fetch(`/cryptography/${cryptType}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("ciphertextArea").value = data.ciphertext;
      })
      .catch((error) => {
        console.error(`Error:`, error);
      });
  });
}

enableTextarea();
encryptText();
