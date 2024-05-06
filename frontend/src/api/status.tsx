export async function getStatus(): Promise<String>{
  return (await fetch("http://localhost:5000/api/status")).json();
}
