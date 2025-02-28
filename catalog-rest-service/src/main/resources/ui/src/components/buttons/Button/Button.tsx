/*
  * Licensed to the Apache Software Foundation (ASF) under one or more
  * contributor license agreements. See the NOTICE file distributed with
  * this work for additional information regarding copyright ownership.
  * The ASF licenses this file to You under the Apache License, Version 2.0
  * (the "License"); you may not use this file except in compliance with
  * the License. You may obtain a copy of the License at

  * http://www.apache.org/licenses/LICENSE-2.0

  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
*/

import React, { FunctionComponent } from 'react';
// import classnames from 'classnames';
import { ButtonProps, Ref } from './Button.interface';
import { button } from './Button.styles';

export const Button: FunctionComponent<ButtonProps> = React.forwardRef<
  Ref,
  ButtonProps
>(
  (
    {
      block = false,
      children,
      className = '',
      disabled = false,
      size,
      tag = 'button',
      theme = 'default',
      type = tag === 'button' ? 'button' : undefined,
      variant,
      ...other
    }: ButtonProps,
    ref
  ) => {
    const baseStyle = button.base;
    const blockStyle = button.block;
    const sizeStyles = button.size[size];
    const layoutStyles = button[variant][theme].base;
    const activeStyles = button[variant][theme].active;
    const disabledStyles = button[variant][theme].disabled;
    const classes = [
      baseStyle,
      sizeStyles,
      layoutStyles,
      disabled ? disabledStyles : activeStyles,
      block ? blockStyle : '',
      className,
    ].join(' ');

    return React.createElement(
      tag,
      {
        className: classes,
        ref,
        disabled,
        type,
        ...other,
      },
      children
    );
  }
);

Button.displayName = 'Button';
