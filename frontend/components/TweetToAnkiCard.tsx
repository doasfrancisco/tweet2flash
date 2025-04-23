'use client'

import React, { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { fetchTweetCard } from '@/app/lib/api'
import { Copy, Check } from 'lucide-react'

export default function TweetToAnkiCard() {
  const [tweetUrl, setTweetUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    front: string
    back: string
    link: string
  } | null>(null)
  const [copied, setCopied] = useState<'front' | 'back' | null>(null)

  const handleSubmit = async () => {
    if (!tweetUrl) return
    setLoading(true)
    try {
      const card = await fetchTweetCard([tweetUrl])
      setResult(card)
    } catch (err) {
      console.error('Failed to fetch card:', err)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text: string, field: 'front' | 'back') => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(field)
      setTimeout(() => setCopied(null), 2000)
    })
  }

  return (
    <div className="max-w-xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-semibold text-center">🧠 Tweet → Anki Card</h1>
      <div className="space-y-4">
        <Input
          placeholder="Paste tweet URL..."
          value={tweetUrl}
          onChange={(e) => setTweetUrl(e.target.value)}
        />
        <Button onClick={handleSubmit} disabled={loading} className="w-full">
          {loading ? 'Processing...' : 'Generate Card'}
        </Button>
      </div>

      {result && (
        <Card className="mt-6">
          <CardContent className="space-y-4 pt-4">
            <div>
              <div className="flex justify-between items-center mb-1">
                <h2 className="font-semibold">Front:</h2>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="h-8 px-2 text-xs"
                  onClick={() => copyToClipboard(result.front, 'front')}
                >
                  {copied === 'front' ? (
                    <>
                      <Check className="h-4 w-4 mr-1" />
                      Copied
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4 mr-1" />
                      Copy
                    </>
                  )}
                </Button>
              </div>
              <Textarea readOnly value={result.front} className="bg-muted" />
            </div>
            <div>
              <div className="flex justify-between items-center mb-1">
                <h2 className="font-semibold">Back:</h2>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="h-8 px-2 text-xs"
                  onClick={() => copyToClipboard(
                    `${result.back}\n\nLink: ${result.link}`, 
                    'back'
                  )}
                >
                  {copied === 'back' ? (
                    <>
                      <Check className="h-4 w-4 mr-1" />
                      Copied
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4 mr-1" />
                      Copy
                    </>
                  )}
                </Button>
              </div>
              <Textarea
                readOnly
                value={`${result.back}\n\nLink: ${result.link}`}
                className="bg-muted"
              />
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}