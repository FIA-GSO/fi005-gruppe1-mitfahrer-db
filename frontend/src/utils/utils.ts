const apiUrl = "http://127.0.0.1:5000/"

function getErrorMessage(status: Number) {
    switch (status) {
      case 403:
        return "Entschuldigung, das hat nicht geklappt. Bitte prüfen Sie Ihre Anmeldedaten und versuchen Sie es erneut.";
      case 500:
      case 502:
      case 404:
        return "Entschldigung, er Server kann die Anfrage im Moment nicht bearbeiten. Bitte versuchen Sie es später erneut.";
      default:
        return "Entschuldigung, der Server konnte nicht erreicht werden. Bitte versuchen Sie es später erneut.";
    }
  }

const API = async (endpoint: string, method: string = "GET", body?: any) => {
    const res = await fetch(apiUrl + endpoint, {
        credentials: "include",
        method,
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body
    })
    if (!res.ok) {
        throw new Error(getErrorMessage(res.status))
    }
    return res
}

export {API, getErrorMessage}