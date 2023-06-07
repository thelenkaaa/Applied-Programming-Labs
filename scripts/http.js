export async function makeRequest(url, method, body = null, headers = {}) {
    console.log('Hello')
    const DefaultHeaders = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      };
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...DefaultHeaders,
        ...headers,
      },
      body: body && JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
