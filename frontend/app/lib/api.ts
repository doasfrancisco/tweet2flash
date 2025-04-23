export async function fetchTweetCard(urls: string[]) {
  const res = await fetch('/api/flashcard', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ urls }),
  });

  if (!res.ok) {
    throw new Error('Failed to fetch flashcard');
  }

  const json = await res.json();
  return {
    front: json.front,
    back: json.back,
    link: extractLinkFromBack(json.back),
  };
}

function extractLinkFromBack(back: string): string {
  const match = back.match(/https?:\/\/\S+/);
  return match ? match[0] : '';
}