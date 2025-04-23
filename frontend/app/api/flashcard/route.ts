import { NextResponse } from 'next/server';

const API_URL = process.env.API_URL
const CODE = process.env.CODE;

export async function POST(request: Request) {
    const { urls } = await request.json();
    
    try {
      const res = await fetch(`${API_URL}?code=${CODE}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls }),
      });
      
      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }
      
      const data = await res.json();
      return NextResponse.json(data);
    } catch (error) {
      console.error('Error fetching flashcard:', error);
      return NextResponse.json(
        { error: 'Failed to fetch flashcard' },
        { status: 500 }
      );
    }
  }