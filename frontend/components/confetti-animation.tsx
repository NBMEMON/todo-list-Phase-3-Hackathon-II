'use client';

import React, { useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';

interface ConfettiAnimationProps {
  isActive: boolean;
  particleCount?: number;
  spread?: number;
  startVelocity?: number;
}

export default function ConfettiAnimation({
  isActive,
  particleCount = 150,
  spread = 70,
  startVelocity = 30
}: ConfettiAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (isActive) {
      confetti({
        particleCount,
        spread,
        startVelocity,
        origin: { y: 0.6 },
        zIndex: 10000,
      });
    }
  }, [isActive, particleCount, spread, startVelocity]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full pointer-events-none"
      style={{ display: isActive ? 'block' : 'none', zIndex: 9999 }}
    />
  );
}